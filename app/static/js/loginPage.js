function freeAccount() {}
function login() {
  const loginFormDOM = document.getElementById("loginFormContainer");
  closeLandingContent();
  closeSupport();

  setTimeout(() => {
    loginFormDOM.classList.remove("loginFormClose");
    loginFormDOM.classList.add("loginFormPopUp");
  }, 1000);
  const loginButton = document.getElementsByClassName("loginButton");
  loginButton[0].classList.add("responsiveLoginButton");
  changeLogin(1, null);
}
function closeHomePage() {
  closeLandingContent();
  closeLogin();
  closeSupport();
  document
    .getElementById("homePageHeader")
    .classList.add("homePageHeaderClose");
  setTimeout(() => {
    document.getElementById("homePage").classList.add("homePageClose");
  }, 1500);
}
function closeLandingContent() {
  document
    .getElementById("homePageContent")
    .classList.add("homePageContentCloseContent");
}
function closeLogin() {
  document.getElementById("loginFormContainer").classList.add("loginFormClose");
}
function closeSupport() {
  document.getElementById("supportPage").classList.remove("supportPageOpen");
}
function changeLogin(isLogin, event) {
  if (event) event.preventDefault();
  const effectLoginType = document.getElementById("formType");
  const loginForm = document.getElementById("loginForm");
  const loginFormFields = document.getElementsByClassName("loginFormField");
  const loginButton = document.getElementsByClassName("loginButton");
  if (isLogin === 2) {
    effectLoginType.classList.add("selectRegister");
    effectLoginType.classList.add("formTypeRegister");
    loginForm.style.width = "65%";
    loginForm.style.height = "75%";
    if (!loginButton[1].classList.contains("responsiveLoginButton")) {
      loginButton[1].classList.add("responsiveLoginButton");
        }
    loginButton[0].classList.remove("responsiveLoginButton");
        for (let index = 0; index < loginFormFields.length; index++) {
      loginFormFields[index].classList.remove("hiddenLoginField");
        }
        loginForm.onsubmit = handleRegister;
    } else {
    effectLoginType.classList.remove("selectRegister");
    effectLoginType.classList.remove("formTypeRegister");
    loginForm.style.width = "50%";
    loginForm.style.height = "70%";
    loginButton[0].classList.add("responsiveLoginButton");
    loginButton[1].classList.remove("responsiveLoginButton");
    loginFormFields[0].classList.add("hiddenLoginField");
    loginFormFields[3].classList.add("hiddenLoginField");
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
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username_or_email: username,
            password: password,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Login successful") {
            alert("Login successful");
            localStorage.setItem('user_id', data.user_id);
            localStorage.setItem('username', data.username);
            localStorage.setItem('isPremium', data.premium_id);
            localStorage.setItem('email', data.email);
            updateUserUI(data.username, data.email, data.premium_id, data.remain_days);
            checkIfUserLogin();
            if (data.svg_content) {
                loadSVGContent(data.svg_content);
            }
            
            closeHomePage();
            setTimeout(()=>{document.getElementById('RecommendTooltip').classList.add('tooltipShow')},1500)
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
function checkIfUserLogin(){
    const username = localStorage.getItem('username');
    const loginStatusDiv = document.getElementById('logoutStatus');
    if ( username) {
        loginStatusDiv.innerHTML = '<div class="menu_item" id="handleLogout" onclick="handleLogout()">Log out</div>';
    }   else {
        // Nếu chưa đăng nhập, hiển thị nút hoặc thông báo đăng nhập lại
        loginStatusDiv.innerHTML = '';
    }
}
function checkIfUserTrial() {
    const userId = localStorage.getItem('user_id');
    const username = localStorage.getItem('username');
    const loginStatusDiv = document.getElementById('loginStatus');
    
    if (userId && username) {
        loginStatusDiv.innerHTML = ''; // Xóa nội dung của div

    } else {
        // Nếu chưa đăng nhập, hiển thị nút hoặc thông báo đăng nhập lại
        loginStatusDiv.innerHTML = '<div class="menu_item" id="relogin" onclick="relogin()">Login</div>';
    }
}
function relogin() {
    // Thực hiện hành động đăng nhập lại
    window.location.href = "/"
}
function handleLogout() {
    console.log("Logout function called");

    // Xóa các thông tin lưu trữ trong localStorage
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    localStorage.removeItem('email');
    localStorage.removeItem('premium_id');

    // Chuyển hướng về trang chủ
    window.location.href = "/";
}

function loadSVGContent(svgContent) {
    if (svgCanvas && typeof svgCanvas.setSvgString === 'function') {
        svgCanvas.setSvgString(svgContent);
    } else {
        console.error("svgCanvas or setSvgString method is not available");
    }
}

function handleRegister(event) {
    event.preventDefault();
  const email = document.getElementById("email").value;
  const username = document.getElementById("userName").value;
  const password = document.getElementById("password").value;
  const rePassword = document.getElementById("rePass").value;

    if (!email || !username || !password || !rePassword) {
    alert("Please fill in all fields");
        return;
    }

    if (password !== rePassword) {
    alert("Passwords do not match");
        return;
    }

  fetch("/register", {
    method: "POST",
        headers: {
      "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email,
            username: username,
      password: password,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "User registered successfully!") {
        alert("Registration successful! You can now log in.");
            // Optionally, switch to login form here
        changeLogin(1, new Event("click"));
        } else {
        alert(data.message || "Registration failed. Please try again.");
        }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    });
}

function resetPage() {
  location.reload();
}
function validateLogin(form) {
    event.preventDefault(); // Prevent form submission

  const email = document.getElementById("email").value;
  const username = document.getElementById("userName").value;
  const password = document.getElementById("password").value;
  const rePassword = document.getElementById("rePass").value;

    // Check if it's a registration
  if (
    !document.getElementById("formType").classList.contains("selectRegister")
  ) {
        // This is a login, we'll handle it later
    console.log("Login not implemented yet");
        return false;
    }

    // Validate registration fields
    if (!email || !username || !password || !rePassword) {
    alert("Please fill in all fields");
        return false;
    }

    if (password !== rePassword) {
    alert("Passwords do not match");
        return false;
    }

    // Call the registration API
    registerUser(email, username, password);

    return false; // Prevent form submission
}

function registerUser(email, username, password) {
  fetch("/register", {
    method: "POST",
        headers: {
      "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email,
            username: username,
      password: password,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "User registered successfully!") {
        alert("Registration successful! You can now log in.");
            // Optionally, switch to login form here
        changeLogin(1, new Event("click"));
        } else {
        alert(data.message || "Registration failed. Please try again.");
        }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    });
}

function closeAllExceptTab(type) {
    switch (type) {
        case 1:
      closeHomePage();
            break;
        case 2:
      login();
            break;
        case 3:
      closeLandingContent();
      closeLogin();
      setTimeout(() => {
        document.getElementById("supportPage").classList.add("supportPageOpen");
      }, 1000);
            break;
        default:
            break;
    }
}
function openQuestion(ulNo) {
  questionIcon = document.getElementsByClassName("questionIcon");
  qna = document.getElementsByClassName("qna");
  if (questionIcon[ulNo].classList.contains("rotateSVG")) {
    questionIcon[ulNo].classList.remove("rotateSVG");
    qna[ulNo].classList.remove("qnaOpen");
    return;
  }
  questionIcon[ulNo].classList.add("rotateSVG");
  qna[ulNo].classList.add("qnaOpen");
        return;
    }
function openTutorial(type = 0) {
  const isPremium = Number(localStorage.getItem('isPremium'));
  if (![1,2,3,4,5].includes(isPremium) && type === 1) {
    document.getElementById('tutorialContainer').classList.add('hidePayment')
    document.getElementById('questionAnswer').classList.add('hidePayment')
    document.getElementById('contactContainer').classList.add('hidePayment')
  } else{
    document.getElementById('tutorialContainer').classList.remove('hidePayment')
    document.getElementById('questionAnswer').classList.remove('hidePayment')
    document.getElementById('contactContainer').classList.remove('hidePayment')
  }
  document.getElementById("homePage").classList.remove("homePageClose");
  closeTooltip(0)
  setTimeout(() => {
    document
      .getElementById("homePageHeader")
      .classList.remove("homePageHeaderClose");
    document.getElementById("supportPage").classList.add("supportPageOpen");
    const navItem = document.getElementsByClassName("nav-item");
    for (let index = 0; index < navItem.length - 1; index++) {
      navItem[index].classList.add("onReturn");
    }
    navItem[navItem.length - 1].classList.add("openReturn");
  }, 1000);
}
function paymentRequest(premium_id) {
  const userId = localStorage.getItem("user_id");

  if (!userId) {
    alert("Bạn cần đăng nhập trước khi thực hiện thanh toán.");
    return;
  }

  fetch("/create_payment", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: userId,
      premium_id: premium_id,
    }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.payment_url) {
        window.location.href = data.payment_url;
      } else {
        alert("Tạo thanh toán không thành công: " + data.message);
      }
    })
    .catch(error => {
      console.error("Yêu cầu thanh toán thất bại:", error);
      alert("Lỗi trong quá trình xử lý thanh toán. Vui lòng thử lại.");
    });
}

function getPremiumTypeName(premium_id) {
    switch (Number(premium_id)) {
        case 1:
            return "Trial";
        case 2:
        case 3:
            return "Cá Nhân";
        case 4:
        case 5:
            return "Doanh Nghiệp";
        default:
            return "Free";
    }
}

function updateUserUI(username, email, premium_id, remain_days) {
  const userInfoDisplay = document.getElementById('user_info_display');
  userInfoDisplay.innerHTML = `
      <strong>Username:</strong> ${username} <br>
      <strong>Email:</strong> ${email} <br>
      <strong>Premium ID:</strong> ${premium_id} <br>
      ${remain_days !== null ? `<strong>Remaining Days:</strong> ${remain_days} <br>` : ''}
  `;
}
// Tự động tải thông tin người dùng nếu đã có trong localStorage (ví dụ: khi tải lại trang)
window.onload = function() {
    const savedUsername = localStorage.getItem('username');
    const savedEmail = localStorage.getItem('email');
    const savedPremiumId = localStorage.getItem('premium_id');
    if (savedUsername && savedEmail && savedPremiumId) {
        updateUserUI(savedUsername, savedEmail, savedPremiumId);
    }
};

function showPremiumNeedNesting(){
    const isPremium = Number(localStorage.getItem('isPremium'));
    if (![1,2,3,4,5].includes(isPremium)) {
        document.getElementById('tooltip').classList.add('tooltipShow')
        return;
      }
  }
  function closeTooltip(typeTooltip){
    typeTooltip === 0 ? document.getElementById('tooltip').classList.remove('tooltipShow') : document.getElementById('RecommendTooltip').classList.remove('tooltipShow')
    return;
}
  localStorage.clear();

function saveSVGSource() {
    const userId = localStorage.getItem("user_id");
    const svgContent = svgCanvas.getSvgString();

    if (!userId) {
        alert("Please log in to save your SVG source.");
        return;
    }

    fetch("/save_svg_source", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: userId,
            svg_content: svgContent
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "SVG source saved successfully") {
            alert("SVG source saved successfully!");
        } else {
            alert("Failed to save SVG source: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while saving the SVG source. Please try again.");
    });
}