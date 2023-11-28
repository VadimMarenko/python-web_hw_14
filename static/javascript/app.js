token = localStorage.getItem('accessToken')


const get_users = async () => {  
  const response = await fetch(`http://localhost:8000/api/users`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  console.log(response.status, response.statusText)
  if (response.status === 200) {
    result = await response.json()
    users.innerHTML = ''
    for (user of result) {
      el = document.createElement('li')
      el.className = 'list-group-item'
      el.innerHTML = `Id: ${user.id} email: ${user.email}`
      users.appendChild(el)
    }
  }
}


const birthday_users = async () => {  
  const response = await fetch(`http://localhost:8000/api/users/birthdays/`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  console.log(response.status, response.statusText)
  if (response.status === 200) {
    result = await response.json()
    
    // const birthdaysElement = document.getElementById("birthdays");
    birthdays.innerHTML = ''
    for (user of result) {
      el = document.createElement('li')
      el.className = 'list-group-item'
      el.innerHTML = `Id: ${user.id} email: ${user.email} birthday: ${user.born_date}`
      birthdays.appendChild(el)
    }
  }
}

get_users()
birthday_users()


// async function submitForm() {
  const get_user = async () => {
    try {
      const userId = 2;
      const apiUrl = `http://localhost:8000/api/users/2`;     
      
      const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      console.log(response.status, response.statusText);
  
      if (response.status === 200) {
        const user = await response.json()
    
        const getUserContainer = document.getElementById('getUser');
        getUserContainer.innerHTML = ''
    
        const userList = document.createElement('ul');
        userList.className = 'user-list';

        for (const prop in user) {
          const listItem = document.createElement('li');
          listItem.innerHTML = `<strong>${prop}:</strong> ${user[prop]}`;
          userList.appendChild(listItem);
        }
        getUserContainer.appendChild(userList);
      } else {
        console.error('Помилка при виконанні запиту:', response.statusText);
      }
    } catch (error) {
      console.error('Помилка при виконанні запиту:', error);
    }
  }
// }
get_user()
// const userIdForm = document.getElementById('userIdForm');

// userIdForm.addEventListener('submit', async (e) => {
//   e.preventDefault();

//   // Отримання значення поля пошуку
//   const userId = userIdForm.elements['userId'].value;

//   try {
//     const response = await fetch(`http://localhost:8000/api/users/search/${userId}`, {
//       method: 'GET',
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     });

//     if (response.ok) {
//       const result = await response.json();
//       console.log('Результат пошуку користувача:', result);
//       // Тут ви можете обробити результати пошуку, наприклад, відобразити їх на сторінці
//     } else {
//       console.error('Помилка при виконанні пошуку:', response.statusText);
//     }
//   } catch (error) {
//     console.error('Помилка при виконанні запиту:', error);
//   }
// });

// const search_user = async () => {
//   search.addEventListener('submit', async (e) => {
//     e.preventDefault()
//     const searchData = {
//       data: searchForm.elements['search'].value,
//     };
//     const queryParams = new URLSearchParams(searchData);
//     const response = await fetch('http://localhost:8000/api/users/{user_id}', {
//       method: 'GET',
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     })
//     if (response.status === 200) {
//       console.log('Результат пошуку користувача')
//       result = await response.json()
//       search.innerHTML = ''
//       for (user of result) {
//         el = document.createElement('li')
//         el.className = 'list-group-item'
//         el.innerHTML = `ID: ${user.id} first_name: ${user.first_name} last_name: ${user.last_name} email: ${user.email}`
//         search.appendChild(el)
//       }
//     }
//   }
//   )
// }
