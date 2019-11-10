const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');

function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        var cookieName = 'theme';
        var cookieValue = 'dark';
        var myDate = new Date();
        myDate.setMonth(myDate.getMonth() + 12);
        document.cookie = cookieName +"=" + cookieValue + ";expires=" + myDate + ";domain=doresko.pythonanywhere.com;path=/";
        location.reload();
        localStorage.setItem('theme', 'dark');
    }
    else {
        document.documentElement.setAttribute('data-theme', 'light');
        var cookieName = 'theme';
        var cookieValue = 'light';
        var myDate = new Date();
        myDate.setMonth(myDate.getMonth() + 12);
        document.cookie = cookieName +"=" + cookieValue + ";expires=" + myDate + ";domain=doresko.pythonanywhere.com;path=/";
        location.reload();
        localStorage.setItem('theme', 'light');
    }
}

toggleSwitch.addEventListener('change', switchTheme, false);

const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'dark') {
        toggleSwitch.checked = true;
    }
}