
			username = form.cleaned_data.get('username')
			messages.success(request, f"New account created: {username}")
			login(request, user)
			messages.info(request, f'You are now logged in as {username}')
			return redirect("main:homepage")
		