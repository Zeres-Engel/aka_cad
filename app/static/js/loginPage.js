function freeAccount(){

}
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
    changeLogin(1,null)
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
    if(event) event.preventDefault();
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
        loginForm.onsubmit = handleRegister;
    } else {
        effectLoginType.classList.remove('selectRegister')
        effectLoginType.classList.remove('formTypeRegister')
        loginForm.style.width='50%'
        loginForm.style.height='70%'
        loginButton[0].classList.add('responsiveLoginButton')
        loginButton[1].classList.remove('responsiveLoginButton')
        loginFormFields[0].classList.add('hiddenLoginField')
        loginFormFields[3].classList.add('hiddenLoginField')
        loginForm.onsubmit = handleLogin;
    }
}

function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById("userName").value;
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Please fill in all fields");
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username_or_email: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Login successful") {
            alert("Login successful");
            localStorage.setItem('user_id', data.user_id);
            localStorage.setItem('username', data.username);
            localStorage.setItem('isPremium', data.isPremium);
            closeHomePage();
            // Redirect or update UI as needed
            // For example: window.location.href = "/dashboard";
        } else if (data.message === "Incorrect password") {
            alert("Login failed: Incorrect password");
        } else if (data.message === "Account does not exist in the system") {
            alert("Login failed: Account does not exist in the system");
        } else {
            alert("Login failed: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
}

function handleRegister(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const username = document.getElementById('userName').value;
    const password = document.getElementById('password').value;
    const rePassword = document.getElementById('rePass').value;

    if (!email || !username || !password || !rePassword) {
        alert('Please fill in all fields');
        return;
    }

    if (password !== rePassword) {
        alert('Passwords do not match');
        return;
    }

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            username: username,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "User registered successfully!") {
            alert('Registration successful! You can now log in.');
            // Optionally, switch to login form here
            changeLogin(1, new Event('click'));
        } else {
            alert(data.message || 'Registration failed. Please try again.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}

function resetPage(){
    location.reload()   
}
function validateLogin(form){
    event.preventDefault(); // Prevent form submission

    const email = document.getElementById('email').value;
    const username = document.getElementById('userName').value;
    const password = document.getElementById('password').value;
    const rePassword = document.getElementById('rePass').value;

    // Check if it's a registration
    if (!document.getElementById('formType').classList.contains('selectRegister')) {
        // This is a login, we'll handle it later
        console.log('Login not implemented yet');
        return false;
    }

    // Validate registration fields
    if (!email || !username || !password || !rePassword) {
        alert('Please fill in all fields');
        return false;
    }

    if (password !== rePassword) {
        alert('Passwords do not match');
        return false;
    }

    // Call the registration API
    registerUser(email, username, password);

    return false; // Prevent form submission
}

function registerUser(email, username, password) {
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            username: username,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "User registered successfully!") {
            alert('Registration successful! You can now log in.');
            // Optionally, switch to login form here
            changeLogin(1, new Event('click'));
        } else {
            alert(data.message || 'Registration failed. Please try again.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
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
function paymentRequest(amount) {
    // Kiểm tra xem người dùng đã đăng nhập chưa
    const userId = localStorage.getItem('user_id'); // Lấy user_id từ localStorage

    if (!userId) {
        // Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập
        alert('Bạn cần đăng nhập trước khi thực hiện thanh toán.');
        window.location.href = '/'; // Giả định đường dẫn đến trang đăng nhập là '/login'
        return;
    }

    // Gửi yêu cầu thanh toán tới server
    fetch('/payment/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,  // Truyền user_id của người dùng
            amount: amount    // Giá tiền gói dịch vụ
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.payment_url) {
            // Chuyển người dùng đến trang thanh toán của PayOS
            window.location.href = data.payment_url;
        } else {
            alert('Tạo thanh toán không thành công: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Yêu cầu thanh toán thất bại:', error);
        alert('Lỗi trong quá trình xử lý thanh toán. Vui lòng thử lại.');
    });
}
