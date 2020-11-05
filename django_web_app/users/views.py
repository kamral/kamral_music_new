from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

#Функция регистрации
def register(request):
    # Проверка , что есть запрос на POST
    if request.method == 'POST':
        # Создаем форму, в качестве параметра передаём ему то,
        # что у нас было в POST запросе и делаем валидацию формы.
        form = UserRegisterForm(request.POST)
        # Валидация данных из формы
        # Если валидация прошла успешно, то сохраняем пользователя
        # и передаем сообщение :
        # Ваша учетная запись создана.
        # Теперь вы моежете войти в систему

        if form.is_valid():
            # Сохраняем пользователя
            form.save()
            # очищаем от мусора и выводим и берем з
            # арегистрированного пользователя
            username = form.cleaned_data.get('username')
            # и передаем сообщение :
            # Ваша учетная запись создана.
            # Теперь вы моежете войти в систему

            messages.success(request, f'Ваша учетная запись была создана!'
                                      f' Теперь вы можете войти в систему')
            # Перенаправляем по ulr на логин
            return redirect('login')

    else:
        # отправляем готовую форму
        form = UserRegisterForm()
        # передаем форму по рендерингу
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш аккаунт был обновлен')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
