function fetchDataAndPopulateDropdowns(userStartingLetter, businessStartingLetter) {
    let userDropdown = document.getElementById('user_id');
    let businessDropdown = document.getElementById('business_id');
    let loadMoreBusinessButton = document.getElementById('loadMoreBusiness');
    let loadMoreUserButton = document.getElementById('loadMoreUser');

    // Clear existing options
    userDropdown.innerHTML = '<option value="" disabled selected>Select User ID</option>';
    businessDropdown.innerHTML = '<option value="" disabled selected>Select Business ID</option>';

    let currentPageUser = 1;
    let currentPageBusiness = 1;
    let itemsPerPage = 10; // Adjust this based on your preference

    function loadUserData(page) {
        console.log('Fetching user data for page:', page);
        fetch(`/fetch_user_data?page=${page}&user_start=${userStartingLetter}`, {
            method: 'GET', // Use the appropriate HTTP method (e.g., 'GET' or 'POST')
        })
            .then(response => response.json())
            .then(data => {
                console.log('Received user data:', data);
                data.user_data.forEach(user => {
                    let option = document.createElement('option');
                    option.text = user;
                    option.value = user;
                    userDropdown.add(option);
                });

                if (data.hasMore) {
                    // If there are more items, show the "Load More" button
                    loadMoreUserButton.style.display = 'block';
                } else {
                    // If no more items, hide the "Load More" button
                    loadMoreUserButton.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });
    }

    function loadBusinessData(page) {
        console.log('Fetching business data for page:', page);
        fetch(`/fetch_business_data?page=${page}&business_start=${businessStartingLetter}`, {
            method: 'GET', // Use the appropriate HTTP method (e.g., 'GET' or 'POST')
        })
            .then(response => response.json())
            .then(data => {
                console.log('Received business data:', data);
                data.business_data.forEach(business => {
                    let option = document.createElement('option');
                    option.text = business;
                    option.value = business;
                    businessDropdown.add(option);
                });

                if (data.hasMore) {
                    // If there are more items, show the "Load More" button
                    loadMoreBusinessButton.style.display = 'block';
                } else {
                    // If no more items, hide the "Load More" button
                    loadMoreBusinessButton.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error fetching business data:', error);
            });
    }

    // Load initial data
    loadUserData(currentPageUser);
    loadBusinessData(currentPageBusiness);

    // Attach event listener to the "Load More" buttons
    loadMoreUserButton.addEventListener('click', function () {
        currentPageUser++;
        loadUserData(currentPageUser);
    });

    loadMoreBusinessButton.addEventListener('click', function () {
        currentPageBusiness++;
        loadBusinessData(currentPageBusiness);
    });
}
