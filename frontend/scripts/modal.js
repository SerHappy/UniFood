function setupModal() {
    console.log("Setting up modal...");
    const modal = document.getElementById('modal');
    const btnLogin = document.getElementById("modalTrigger");
    const toRegisterBtn = document.getElementById("toRegister");
    const closeSpans = document.getElementsByClassName("close");

    btnLogin.onclick = () => {
        modal.style.display = "flex";
        document.getElementById("loginForm").style.display = "block";
        document.getElementById("registerForm").style.display = "none";
    }

    toRegisterBtn.onclick = () => {
        document.getElementById("loginForm").style.display = "none";
        document.getElementById("registerForm").style.display = "block";
    }

    Array.from(closeSpans).forEach(closeSpan => {
        closeSpan.onclick = () => {
            modal.style.display = "none";
        }
    });

    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
    console.log("Modal setup complete.");
}
