from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PasswordChangeForm, ManagementStaffCreationForm, SearchStaffForm, GenerateVoucherForm
from django.contrib.auth import authenticate, update_session_auth_hash
from .models import Profile
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import SubscriptionPlanForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import SubscriptionPlan
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .models import SubscriptionTicket


# 404 Error Page.
def custom_page_not_found(request, exception=None):
    return render(request, 'accounts/404.html', status=404)


# 403 Error Page.
def custom_page_forbidden(request, exception=None):
    return render(request, 'accounts/403.html', status=403)


# 500 Error Page.
def custom_server_not_found(request, exception=None):
    return render(request, 'accounts/500.html', status=500)


@login_required(login_url='account-login')
def index(request):

    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'accounts/index.html', context)


@login_required(login_url='account-login')
def user_profile(request):

    context = {
        'page_title': 'Profile',
    }
    return render(request, 'accounts/profile.html', context)


class SubscriptionPlanCreateView(CreateView):
    model = SubscriptionPlan
    template_name = 'accounts/subscription_plan_form.html'
    form_class = SubscriptionPlanForm  # Use the form for creating

    def form_valid(self, form):
        # Save the form and add a success message
        form.save()
        messages.success(self.request, 'Subscription plan updated successfully.')
        return super().form_valid(form)

    success_url = reverse_lazy('subscription-plan-list')


class SubscriptionPlanListView(ListView):
    model = SubscriptionPlan
    template_name = 'accounts/subscription_plan_list.html'
    context_object_name = 'subscription_plans'  # Optional: Use a custom name for the object_list
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['additional_data'] = 'Some additional data you want to pass to the template'
        return context


class SubscriptionPlanDetailView(DetailView):
    model = SubscriptionPlan
    template_name = 'subscription_plan_detail.html'


class SubscriptionPlanUpdateView(UpdateView):
    model = SubscriptionPlan
    template_name = 'subscription_plan_form.html'
    form_class = SubscriptionPlanForm  # Use the form for updating


class SubscriptionPlanDeleteView(DeleteView):
    model = SubscriptionPlan
    template_name = 'subscription_plan_confirm_delete.html'
    success_url = '/subscription-plans/'


def generate_voucher(request):
    if request.method == 'POST':
        form = GenerateVoucherForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data['plan_id']
            duration_days = form.cleaned_data['duration_days']

            # Calculate the expiration date based on the plan duration
            expiration_date = timezone.now() + timedelta(days=int(duration_days))

            # Create a new SubscriptionTicket instance
            subscription_ticket = SubscriptionTicket(plan=plan, expiration_date=expiration_date, duration_days=duration_days)

            # Save the subscription ticket
            subscription_ticket.save()

            # Redirect to a success page or display a success message
            return redirect('voucher-list')

    else:
        form = GenerateVoucherForm()

    context = {
        'form': form,
        'page_title': 'Generate Voucher',
    }

    return render(request, 'accounts/generate_voucher.html', context)


class VoucherListView(ListView):
    model = SubscriptionTicket
    template_name = 'accounts/voucher_list.html'
    context_object_name = 'voucher_list'  # Optional: Use a custom name for the object_list
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['additional_data'] = 'Some additional data you want to pass to the template'
        return context


# Change user password view
@login_required(login_url='accounts-login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['old_password'])
            if user is not None:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # Update session to prevent logout
                messages.success(request, 'Your Password Changed Successfully.')
                return redirect('accounts-password-change-done')  # Redirect to password change success page
            else:
                form.add_error('old_password', 'Incorrect old password')
                messages.warning(request, 'Incorrect old Password.')
    else:
        form = PasswordChangeForm()

    context = {
        'form': form,
        'page_title': 'Change Password',
    }
    return render(request, 'accounts/password_change.html', context)


# Change user password successfully view
@login_required(login_url='accounts-login')
def password_change_done(request):

    context = {
        'page_title': 'Password Changed',
    }
    return render(request, 'accounts/password_change_done.html', context)  


# Create Management Staff user view
@login_required(login_url='accounts-login')
def create_management_staff(request):
    logged_user = request.user
    try:
        user_profile = Profile.objects.select_related('user').get(user=logged_user)
        user_role = user_profile.role
        # Check if logged in user is super admin else don't allow access
        if logged_user.is_superuser or user_role == 'admin':
            if request.method == 'POST':
                
                form = ManagementStaffCreationForm(request.POST)
                
                if form.is_valid():
                    user = form.save()
                    role = form.cleaned_data.get('role')

                    # Get the Created New user's profile
                    profile = Profile.objects.get(user=user)
                    # Update the profile DB role field
                    profile.role = role
                    # Save the changes to the Profile DB
                    profile.save()

                    messages.success(request, f'{role} Created successfully.')
                    return redirect('account-staff-list')
            else:
                form = ManagementStaffCreationForm()
            context = {
                'page_title': 'Create User',
                'form': form
            }
            return render(request, 'accounts/create_user.html', context)
        else:
            return redirect('accounts-dashboard')
    except Profile.DoesNotExist:
        # Handle the case when the profile doesn't exist
        return redirect('accounts-dashboard')


@login_required(login_url='account-login')
def staff_list(request):
    if request.user.is_superuser or request.user.profile.role in ['admin', 'principal']:
        # List of Staff
        staff_list = Profile.objects.filter(Q(role="dean") | Q(role="subject teacher") | Q(role="form master") | Q(role="principal") | Q(is_active=True)).order_by('-last_updated')
        number_of_staff = staff_list.count()

    form = SearchStaffForm(request.GET or None)

    if request.method == "GET" and form.is_valid():
        search_query = form.cleaned_data['search_query']
        # Filter staff users
        staff_list = Profile.objects.filter(
            Q(user__username__icontains=search_query) | Q(phone__icontains=search_query) | Q(full_name__icontains=search_query), Q(role='dean') | Q(role='subject teacher') | Q(role='form master') | Q(role='principal')
        )

    paginator = Paginator(staff_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'List of Staff',
        'staff_list': page_obj,
        'number_of_staff': number_of_staff,
        'form': form,
    }
    return render(request, 'accounts/staff_list.html', context)


# Disable user
@login_required(login_url='account-login')
def disable_user(request, pk):
    if request.user.is_superuser or request.user.profile.role in ['admin']:
        user_to_disable = get_object_or_404(Profile, pk=pk)
        # Change the USER is_active to False
        user_to_disable.is_active = False
        user_to_disable.save()
        messages.error(request, f'{user_to_disable.user.username} Disabled Successfully.')
        return redirect('account-staff-list')


# Enable User
@login_required(login_url='account-login')
def enable_user(request, pk):
    if request.user.is_superuser or request.user.profile.role in ['admin']:
        user_to_enable = get_object_or_404(Profile, pk=pk)
        # Change the USER is_active to False
        user_to_enable.is_active = True
        user_to_enable.save()
        messages.success(request, f'{user_to_enable.user.username} Enabled Successfully.')
        return redirect('account-staff-list')


