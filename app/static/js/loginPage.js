 function login(){
    const loginFormDOM = document.getElementById('loginFormContainer');
    closeLandingContent()
    setTimeout(()=>{loginFormDOM.classList.add('loginFormPopUp');},1000)
    const loginButton = document.getElementsByClassName('loginButton');
    loginButton[0].classList.add('responsiveLoginButton')
}
function closeHomePage(){
    closeLandingContent()
    document.getElementById('loginFormContainer').classList.add('loginFormClose')
    document.getElementById('homePageHeader').classList.add('homePageHeaderClose')
    setTimeout(()=>{document.getElementById('homePage').classList.add('homePageClose')},1500)
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
function validateLogin(form){
    console.log(form);
}

