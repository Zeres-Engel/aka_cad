 function login(){
    const loginFormDOM = document.getElementById('loginFormContainer');
    closeLandingContent()
    closeSupport()

    setTimeout(()=>{
        loginFormDOM.classList.remove('loginFormClose')
        loginFormDOM.classList.add('loginFormPopUp');
    },1000)
    const loginButton = document.getElementsByClassName('loginButton');
    loginButton[0].classList.add('responsiveLoginButton')
}
function closeHomePage(){
    closeLandingContent()
    closeLogin()
    closeSupport()
    document.getElementById('homePageHeader').classList.add('homePageHeaderClose')
    setTimeout(()=>{document.getElementById('homePage').classList.add('homePageClose')},1500)
}
function closeLandingContent(){
    document.getElementById('homePageContent').classList.add('homePageContentCloseContent')
}
function closeLogin(){
    document.getElementById('loginFormContainer').classList.add('loginFormClose')
}
function closeSupport(){
    document.getElementById('supportPage').classList.remove('supportPageOpen')
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
function closeAllExceptTab(type){
    switch (type) {
        case 1:
            closeHomePage()
            break;
        case 2:
            login()
            break;
        case 3:
            closeLandingContent()
            closeLogin()
            setTimeout(()=>{document.getElementById('supportPage').classList.add('supportPageOpen')},1000)
            break;
        default:
            break;
    }
}
function openQuestion(ulNo){
    questionIcon = document.getElementsByClassName('questionIcon')
    qna = document.getElementsByClassName('qna')
    if (questionIcon[ulNo].classList.contains('rotateSVG')) {
        questionIcon[ulNo].classList.remove('rotateSVG')
        qna[ulNo].classList.remove('qnaOpen')
        return;
    }
    questionIcon[ulNo].classList.add('rotateSVG')
    qna[ulNo].classList.add('qnaOpen')
    return;
}
function openTutorial(){
    document.getElementById('homePage').classList.remove('homePageClose')
    setTimeout(()=>{
        document.getElementById('homePageHeader').classList.remove('homePageHeaderClose');
        document.getElementById('supportPage').classList.add('supportPageOpen');
        const navItem = document.getElementsByClassName('nav-item');
        for (let index = 0; index < navItem.length-1; index++) {
            navItem[index].classList.add('onReturn')
        }
        navItem[navItem.length-1].classList.add('openReturn')
    },1000)
}