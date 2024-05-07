// BUTTON SELECTOR
const btnLight = document.querySelector('.btnLight');

// EVENT LISTENER AND STORAGE OF THE THEME
btnLight.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        if (document.body.classList.contains('light-mode')) {
            localStorage.setItem('theme', 'light-mode');
        } else{
            localStorage.removeItem('theme');
        }
})

// PROPER IMPLEMENTATION OF THE THEME STORAGE
const theme = localStorage.getItem('theme');
if (theme) {
    document.body.classList.add('light-mode');
}