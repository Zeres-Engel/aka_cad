document.addEventListener("DOMContentLoaded", function() {
    const svgcanvas = document.getElementById('svgcanvas');

    function gatherSVGData() {
        return svgcanvas.innerHTML; // Thu thập dữ liệu SVG từ svgcanvas
    }

    function sendDataToServer() {
        console.log('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
        const svgData = gatherSVGData();

        fetch('/nest', { // Đổi URL để gọi đúng route trong Flask
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ svg: svgData }) // Gửi dữ liệu SVG dưới dạng JSON
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    document.getElementById('nest').addEventListener('click', sendDataToServer);

});
