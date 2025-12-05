from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Menu, MenuItem
from .forms import MenuForm, MenuItemForm


def login_view(request):
    """Custom login view with clean UI"""
    if request.user.is_authenticated:
        return redirect('menu_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'menu_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'menu_builder/login.html')


def signup_view(request):
    """Custom signup view with clean UI"""
    if request.user.is_authenticated:
        return redirect('menu_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'menu_builder/signup.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Dashboard view for authenticated users"""
    from django.contrib.auth.models import User
    
    # Get statistics
    total_menus = Menu.objects.count()
    total_users = User.objects.count()
    
    # Try to get page count, handle if wagtailcore is not available
    try:
        from wagtailcore.models import Page
        total_pages = Page.objects.live().count()
    except:
        total_pages = 0
    
    # Get recent menus
    recent_menus = Menu.objects.all().order_by('-id')[:5]
    
    context = {
        'total_menus': total_menus,
        'total_users': total_users,
        'total_pages': total_pages,
        'recent_menus': recent_menus,
    }
    
    return render(request, 'menu_builder/dashboard.html', context)


@login_required
def menu_create_view(request):
    """View to create a new menu"""
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            messages.success(request, f'Menu "{menu.title}" created successfully!')
            return redirect('menu_edit', menu_id=menu.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MenuForm()
    
    return render(request, 'menu_builder/menu_form.html', {
        'form': form,
        'title': 'Create New Menu',
        'action': 'Create'
    })


@login_required
def menu_edit_view(request, menu_id):
    """View to edit an existing menu"""
    menu = get_object_or_404(Menu, id=menu_id)
    
    if request.method == 'POST':
        # Check if this is a menu form submission or menu item form submission
        if 'menu_form' in request.POST:
            form = MenuForm(request.POST, instance=menu)
            if form.is_valid():
                menu = form.save()
                messages.success(request, f'Menu "{menu.title}" updated successfully!')
                return redirect('menu_edit', menu_id=menu.id)
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = MenuForm(instance=menu)
    else:
        form = MenuForm(instance=menu)
    
    menu_items = menu.menu_items.all().order_by('sort_order')
    
    return render(request, 'menu_builder/menu_form.html', {
        'form': form,
        'menu': menu,
        'menu_items': menu_items,
        'title': f'Edit Menu: {menu.title}',
        'action': 'Update'
    })


@login_required
def menu_preview_view(request, menu_id):
    """View to preview how the menu will look"""
    menu = get_object_or_404(Menu, id=menu_id)
    # Get all root items (no parent) ordered by sort_order for drag and drop
    root_items = menu.menu_items.filter(parent__isnull=True).order_by('sort_order')
    
    return render(request, 'menu_builder/menu_preview.html', {
        'menu': menu,
        'menu_items': root_items,
    })


@login_required
def menu_reorder_view(request, menu_id):
    """AJAX view to reorder menu items"""
    from django.http import JsonResponse
    import json
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    menu = get_object_or_404(Menu, id=menu_id)
    
    try:
        data = json.loads(request.body)
        item_ids = data.get('item_ids', [])
        
        # Update sort_order for each item based on new order
        for index, item_id in enumerate(item_ids):
            try:
                menu_item = MenuItem.objects.get(id=item_id, menu=menu)
                menu_item.sort_order = index
                menu_item.save()
            except MenuItem.DoesNotExist:
                continue
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def menu_item_add_view(request, menu_id):
    """View to add a new menu item"""
    menu = get_object_or_404(Menu, id=menu_id)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, menu=menu)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.menu = menu
            menu_item.save()
            messages.success(request, f'Menu item "{menu_item.title}" added successfully!')
            return redirect('menu_edit', menu_id=menu.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MenuItemForm(menu=menu)
    
    return render(request, 'menu_builder/menu_item_form.html', {
        'form': form,
        'menu': menu,
        'title': f'Add Menu Item to "{menu.title}"',
        'action': 'Add'
    })


@login_required
def menu_item_edit_view(request, menu_id, item_id):
    """View to edit an existing menu item"""
    menu = get_object_or_404(Menu, id=menu_id)
    menu_item = get_object_or_404(MenuItem, id=item_id, menu=menu)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item, menu=menu)
        if form.is_valid():
            menu_item = form.save()
            messages.success(request, f'Menu item "{menu_item.title}" updated successfully!')
            return redirect('menu_edit', menu_id=menu.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MenuItemForm(instance=menu_item, menu=menu)
    
    return render(request, 'menu_builder/menu_item_form.html', {
        'form': form,
        'menu': menu,
        'menu_item': menu_item,
        'title': f'Edit Menu Item: {menu_item.title}',
        'action': 'Update'
    })


@login_required
def menu_item_delete_view(request, menu_id, item_id):
    """View to delete a menu item"""
    menu = get_object_or_404(Menu, id=menu_id)
    menu_item = get_object_or_404(MenuItem, id=item_id, menu=menu)
    
    if request.method == 'POST':
        item_title = menu_item.title
        menu_item.delete()
        messages.success(request, f'Menu item "{item_title}" deleted successfully!')
        return redirect('menu_edit', menu_id=menu.id)
    
    return render(request, 'menu_builder/menu_item_delete.html', {
        'menu': menu,
        'menu_item': menu_item
    })


@login_required
def menu_delete_view(request, menu_id):
    """View to delete a menu"""
    menu = get_object_or_404(Menu, id=menu_id)
    
    if request.method == 'POST':
        menu_title = menu.title
        menu.delete()
        messages.success(request, f'Menu "{menu_title}" deleted successfully!')
        return redirect('menu_list')
    
    return render(request, 'menu_builder/menu_delete.html', {'menu': menu})


def menu_list_view(request):
    """View to list all menus - Main dashboard"""
    menus = Menu.objects.all().order_by('title')
    
    context = {
        'menus': menus,
    }
    
    return render(request, 'menu_builder/menu_list.html', context)


def get_menu(slug):
    """Helper function to get a menu by slug"""
    try:
        return Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        return None

