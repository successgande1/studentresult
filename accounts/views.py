from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PasswordChangeForm, ManagementStaffCreationForm, SearchStaffForm, GenerateSubscriptionForm
from django.contrib.auth import authenticate, update_session_auth_hash
from .models import Profile
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import (SubscriptionPlanForm,
                    BusinessAccountForm,
                    PINActivationForm,
                    AdminUserCreationForm,
                    ProfileUpdateForm,
                    TeacherCreationForm
                    )
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import SubscriptionPlan, BusinessAccount, SubscriptionHistory
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .models import Subscription
from .helpers import (get_profile, profile_complete)


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
    logged_user = request.user
    # Check if logged in user is admin and profile is completed
    if logged_user.profile.role in ['admin', 'principal', 'dean']:
        profile = get_profile(logged_user)
        if not profile_complete(profile):
            return redirect('account_profile_update')
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'accounts/index.html', context)


@login_required(login_url='account-login')
def user_profile_update(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        # Check if form is valid
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your Profile Updated Successfully')
            return redirect('account_profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form,
        'page_title': 'Profile Update',
    }
    return render(request, 'accounts/update_profile.html', context)


@login_required(login_url='account-login')
def user_profile(request):

    context = {
        'page_title': 'Profile',
    }
    return render(request, 'accounts/profile.html', context)


class SubscriptionPlanCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SubscriptionPlan
    template_name = 'accounts/subscription_plan_form.html'
    form_class = SubscriptionPlanForm  # Use the form for creating

    def form_valid(self, form):
        # Save the form and add a success message
        form.save()
        messages.success(self.request, 'Subscription Plan Created Successfully.')
        return super().form_valid(form)

    success_url = reverse_lazy('subscription-plan-list')

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlanListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = SubscriptionPlan
    template_name = 'accounts/subscription_plan_list.html'
    context_object_name = 'subscription_plans'  # Optional: Use a custom name for the object_list
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Plan List'
        return context

    # function to check if the user is a superuser
    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlanDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = SubscriptionPlan
    template_name = 'accounts/subscription_plan_detail.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Plan Detail'
        return context

    # function to check if the user is a superuser
    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlanUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubscriptionPlan
    template_name = 'accounts/subscription_plan_form.html'
    form_class = SubscriptionPlanForm  # Use the form for updating

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Update Plan'
        return context

    def form_valid(self, form):
        # Save the form and add a success message
        form.save()
        messages.success(self.request, 'Subscription Plan Update Successfully.')
        return super().form_valid(form)

    success_url = reverse_lazy('subscription-plan-list')

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlanDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubscriptionPlan
    template_name = 'accounts/confirm_delete_plan.html'
    success_url = '/subscription-plans/'
    context_object_name = 'plan'  # the context object name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Delete Plan'
        return context

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Subscription plan Deleted successfully.')  # Success message
        return super().delete(request, *args, **kwargs)


class SubscriptionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Subscription
    template_name = 'accounts/confirm_subscription_delete.html'
    success_url = '/subscription/list/'
    context_object_name = 'subscription'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Delete Subscription'
        return context

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.is_superuser


@login_required(login_url='account-login')
def generate_subscription(request):
    if request.method == 'POST':
        form = GenerateSubscriptionForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data['plan_id']
            duration_days = form.cleaned_data['duration_days']

            # Calculate the expiration date based on the plan duration
            expiration_date = timezone.now() + timedelta(days=int(duration_days))

            # Create a new Subscription instance
            subscription_ticket = Subscription(plan=plan, expiration_date=expiration_date, duration_days=duration_days)

            # Save the subscription ticket
            subscription_ticket.save()

            # Redirect to a success page or display a success message
            return redirect('subscription-list')

    else:
        form = GenerateSubscriptionForm()

    context = {
        'form': form,
        'page_title': 'Generate Subscription', 
    }

    return render(request, 'accounts/generate_subscription.html', context)


class SubscriptionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Subscription
    template_name = 'accounts/subscription_list.html'
    context_object_name = 'subscription'  # Optional: Use a custom name for the object_list
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Subscription List'
        return context

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Subscription
    template_name = 'accounts/subscription_detail.html'
    context_object_name = 'subscription'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Subscription Detail'
        return context

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.is_superuser


# Create Business Account View
def create_business_account(request):
    if request.method == 'POST':
        form = BusinessAccountForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            account_type = form.cleaned_data['account_type']
            address = form.cleaned_data['address']
            lga = form.cleaned_data['lga']
            state = form.cleaned_data['state']
            # Check if Business Account already Exist and redirect accordingly
            try:
                business_account = BusinessAccount.objects.get(name=name)
                if business_account.is_active:
                    # Try if Admin User for School already exist and redirect accordingly.
                    try:
                       school_admin = Profile.objects.get(organization=business_account)
                    except Profile.DoesNotExist:
                        messages.warning(request, f'Create Admin User for {business_account} ')
                        return redirect('create_admin_business_user', business_account_id=business_account.pk)
                elif not business_account.is_active:
                    messages.success(request, f'{business_account} needs Subscription ')
                    return redirect('activate_business_account', business_account_id=business_account.pk)
                
            except BusinessAccount.DoesNotExist:
                business_account = BusinessAccount.objects.create(name=name, account_type=account_type, address=address, lga=lga, state=state)
                # Redirect to PIN activation view
                return redirect('activate_business_account', business_account_id=business_account.pk)           
    else:
        form = BusinessAccountForm()
    context = {
        'form': form,
        'page_title': 'Business Acct. Creation',
    }

    return render(request, 'accounts/create_business_account.html', context)


# Business Account Activate Pin view
def pin_activation(request, business_account_id):
    try:
        business_account = BusinessAccount.objects.get(pk=business_account_id)

        if request.method == 'POST':
            form = PINActivationForm(request.POST)
            if form.is_valid():
                # Get the PIN entered by the user
                user_entered_pin = form.cleaned_data['pin']
                
                # Check if the entered PIN matches the stored PIN in the Subscription model
                try:
                    subscription = Subscription.objects.get(pin=user_entered_pin)
                    if subscription:
                        # Check if the subscription is expired
                        if subscription.is_expired():
                            messages.error(request, "Subscription has already expired.")
                            return redirect('activate_business_account')
                        else:
                            # Activate the subscription
                            business_account.is_active = True
                            business_account.subscription_plan = subscription
                            business_account.save()

                            # Record the subscription activation in SubscriptionHistory
                            SubscriptionHistory.objects.create(
                                business_account=business_account,
                                plan=subscription.plan,
                                pin=user_entered_pin,
                                start_date=timezone.now().date(),
                                expiration_date=subscription.expiration_date.date()
                            )
                            messages.success(request, 'Subscription Activated Successfully.')
                            # Redirect to Admin User creation view
                            return redirect('create_admin_business_user', business_account_id=business_account.pk)
                        
                except Subscription.DoesNotExist:
                    # PIN is not found in the Subscription model
                    messages.error(request, "Invalid PIN. Please try again.")
                    return redirect('activate_business_account')
    
        else:
            form = PINActivationForm()
        context = {
            'form': form,
            'page_title': 'Activate Subscription',
        }
        return render(request, 'accounts/pin_activation.html', context)

    except BusinessAccount.DoesNotExist:
        # Handle the case where the business account doesn't exist
        return redirect('create_business_account')


# Business Account Create Admin user view
def create_admin_user(request, business_account_id):
    try:
        business_account = BusinessAccount.objects.get(pk=business_account_id)

        if request.method == 'POST':
            form = AdminUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Try to get the User from the Profile Model and redirect to Login if does not exist
                try:
                    admin_user = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    return redirect('create_business_account')
                else:
                    # Update the Profile of the Admin with his/her organization and role
                    admin_user.organization = business_account
                    admin_user.role = 'admin'
                    admin_user.save()
                    messages.success(request, f'Admin Account Created Successfully for {business_account.name} ')
                    # Redirect to user login page
                    return redirect('account-login')

        else:
            form = AdminUserCreationForm()
        context = {
            'form': form,
            'page_title': 'Create Admin',
        }

        return render(request, 'accounts/create_admin_user.html', context)

    except BusinessAccount.DoesNotExist:
        # Handle the case where the business account doesn't exist
        return redirect('create_business_account')


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
        admin_user_profile = Profile.objects.select_related('user').get(user=logged_user)
        user_role = admin_user_profile.role
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
                    profile.organization = admin_user_profile.organization
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
    

# Create Teacher user view
@login_required(login_url='accounts-login')
def create_teacher_user(request):
    logged_user = request.user
    try:
        admin_user_profile = Profile.objects.select_related('user').get(user=logged_user)
        user_role = admin_user_profile.role
        # Check if logged in user is super admin else don't allow access
        if logged_user.is_superuser or user_role == 'dean':
            if request.method == 'POST':
                
                form = TeacherCreationForm(request.POST)
                
                if form.is_valid():
                    user = form.save()
                    role = form.cleaned_data.get('role')

                    # Get the Created New user's profile
                    profile = Profile.objects.get(user=user)
                    # Update the profile DB role field
                    profile.organization = admin_user_profile.organization
                    profile.role = role
                    # Save the changes to the Profile DB
                    profile.save()

                    messages.success(request, f'{role} Created successfully.')
                    return redirect('account-staff-list')
            else:
                form = TeacherCreationForm()
            context = {
                'page_title': 'Create Teacher',
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


