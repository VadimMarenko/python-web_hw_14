async function submitForm() {
    const form = document.forms[0];

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            first_name: form.first_name.value,
            last_name: form.last_name.value,
            username: form.username.value,
            email: form.email.value,
            password: form.password.value,
            born_date: form.born_date.value,
            description: form.description.value,
        };

        const response = await fetch('http://localhost:8000/api/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        console.log(response.status, response.statusText);

        if (response.ok) {
            const result = await response.json();
            alert(`Congratulations, ${result.user.username}! Your account is created.`);
            // Redirect to "/"
            window.location = '/';
        }
    });
}
