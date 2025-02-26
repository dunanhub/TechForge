// JS для dropdown
const userMenuButton = document.getElementById('user-menu-button');
const dropdownMenu = document.querySelector('.absolute.right-0.z-10.mt-2');

userMenuButton.addEventListener('click', function() {
    dropdownMenu.classList.toggle('hidden');
});

document.addEventListener('click', function(event) {
    if (!userMenuButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.add('hidden');
    }
});
