 function login(){
    const loginFormDOM = document.getElementById('loginFormContainer');
    closeLandingContent()
    setTimeout(()=>{loginFormDOM.classList.add('loginFormPopUp');},2000)
    const loginButton = document.getElementsByClassName('loginButton');
    loginButton[0].classList.add('responsiveLoginButton')
}
function closeHomePage(){
    closeLandingContent()
    document.getElementById('loginFormContainer').classList.add('loginFormClose')
    document.getElementById('homePageHeader').classList.add('homePageHeaderClose')
    setTimeout(()=>{document.getElementById('homePage').classList.add('homePageClose')},3500)
}
function closeLandingContent(){
    document.getElementById('homePageContent').classList.add('homePageContentCloseContent')
}
function changeLogin(isLogin,event){
    event.preventDefault()
    const effectLoginType = document.getElementById('formType')
    const loginForm = document.getElementById('loginForm')
    const loginFormFields = document.getElementsByClassName('loginFormField')
    const loginButton = document.getElementsByClassName('loginButton')
    if ( isLogin === 2 ) {
        effectLoginType.classList.add('selectRegister')
        effectLoginType.classList.add('formTypeRegister')
        loginForm.style.width='65%'
        loginForm.style.height='75%'
        if (!loginButton[1].classList.contains('responsiveLoginButton')) {
            loginButton[1].classList.add('responsiveLoginButton')
        }
        loginButton[0].classList.remove('responsiveLoginButton')
        for (let index = 0; index < loginFormFields.length; index++) {
            loginFormFields[index].classList.remove('hiddenLoginField')
        }
        return;
    }
    if (!loginButton[0].classList.contains('responsiveLoginButton')) {
        loginButton[0].classList.add('responsiveLoginButton')
    }
    loginButton[1].classList.remove('responsiveLoginButton')
    for (let index = 0; index < loginFormFields.length; index++) {
        if(index === 0 || index === 3)
        loginFormFields[index].classList.add('hiddenLoginField')
    }
    loginForm.style.width='50%'
    loginForm.style.height='70%'
    effectLoginType.classList.remove('selectRegister')
}
function resetPage(){
    location.reload()   
}
function changeLogin(type, event) {
    event.preventDefault();
    const formTypeElement = document.getElementById("formType");
    const emailField = document.querySelector(".hiddenLoginField:first-child");
    const rePassField = document.querySelector(".hiddenLoginField:last-child");

    if (type === 1) {
        formTypeElement.textContent = "Login";
        emailField.style.display = "none";
        rePassField.style.display = "none";
        document.getElementById('loginForm').onsubmit = validateLogin;
    } else if (type === 2) {
        formTypeElement.textContent = "Register";
        emailField.style.display = "block";
        rePassField.style.display = "block";
        document.getElementById('loginForm').onsubmit = validateRegister;
    }
}

function validateLogin(form) {
    const username = document.getElementById("userName").value;
    const password = document.getElementById("password").value;

    if (username === "" || password === "") {
        alert("Please fill in all fields");
        return false;
    }

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Login successful");
            window.location.href = "/dashboard"; // Điều hướng tới dashboard sau khi login thành công
        } else {
            alert("Login failed: " + data.message);
        }
    })
    .catch(error => console.error("Error:", error));

    return false; // Ngăn form submit mặc định
}

function validateRegister(form) {
    const email = document.getElementById("email").value;
    const username = document.getElementById("userName").value;
    const password = document.getElementById("password").value;
    const rePass = document.getElementById("rePass").value;

    if (email === "" || username === "" || password === "" || rePass === "") {
        alert("Please fill in all fields");
        return false;
    }

    if (password !== rePass) {
        alert("Passwords do not match");
        return false;
    }

    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Registration successful");
            window.location.href = "/login"; // Điều hướng về login sau khi đăng ký thành công
        } else {
            alert("Registration failed: " + data.message);
        }
    })
    .catch(error => console.error("Error:", error));

    return false; // Ngăn form submit mặc định
}

function validateLogin(form){
    console.log(form);
}

