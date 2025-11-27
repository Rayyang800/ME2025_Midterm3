// --- Modal 開關 ---
function open_input_table() {
    document.getElementById("addModal").style.display = "block";

    // 預設日期為當天
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("date").value = today;

    // 數量預設 = 1
    document.getElementById("quantity").value = 1;

    // 狀態預設 = 未付款
    document.getElementById("status").value = "未付款";
}

function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}


// --- 刪除功能 ---
function delete_data(value) {
    fetch(`/product?order_id=${value}`, {
        method: "DELETE",
    })
    .then(response => response.json())
    .then(result => {
        alert(result.message || "刪除成功");
        location.assign('/');
    })
    .catch(error => console.error("刪除錯誤：", error));
}



// ==============================
//      商品種類 → 商品名稱 (連動)
// ==============================
document.addEventListener("DOMContentLoaded", () => {

    const categorySelect = document.getElementById("category");
    const productSelect  = document.getElementById("product");
    const priceInput     = document.getElementById("price");
    const qtyInput       = document.getElementById("quantity");
    const subtotalInput  = document.getElementById("subtotal");

    // ---------- 1. 選擇 Category → 更新 Product 下拉 ----------
    categorySelect.addEventListener("change", function () {

        let category = this.value;
        if (!category) return;

        fetch(`/product?category=${category}`)
            .then(response => response.json())
            .then(data => {
                productSelect.innerHTML = "";

                data.product.forEach(p => {
                    let opt = document.createElement("option");
                    opt.value = p;
                    opt.textContent = p;
                    productSelect.appendChild(opt);
                });

                // 自動觸發商品名稱 change 取得價格
                productSelect.dispatchEvent(new Event("change"));
            });
    });


    // ---------- 2. 選擇 Product → 更新 Price ----------
    productSelect.addEventListener("change", function () {
        let product = this.value;
        if (!product) return;

        fetch(`/product_price?product=${product}`)
            .then(response => response.json())
            .then(data => {
                priceInput.value = data.price;
                calculateSubtotal();
            });
    });


    // ---------- 3. 數量或單價改變 → 更新小計 ----------
    qtyInput.addEventListener("input", calculateSubtotal);
    priceInput.addEventListener("input", calculateSubtotal);

    function calculateSubtotal() {
        const qty = parseFloat(qtyInput.value) || 0;
        const price = parseFloat(priceInput.value) || 0;
        subtotalInput.value = qty * price;
    }


    // ==============================
    //     表單 POST 提交新增訂單
    // ==============================
    document.getElementById("submit-btn").addEventListener("click", function () {

        let payload = {
            customer_name: document.getElementById("customer").value,
            date: document.getElementById("date").value,
            category: categorySelect.value,
            product: productSelect.value,
            price: parseFloat(priceInput.value),
            quantity: parseInt(qtyInput.value),
            subtotal: parseFloat(subtotalInput.value),
            status: document.getElementById("status").value,
            remark: document.getElementById("remark").value
        };

        if (payload.quantity <= 0) {
            alert("數量必須大於 0！");
            return;
        }

        fetch("/product", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        })
        .then(response => response.json())
        .then(result => {
            alert(result.message || "新增成功！");
            close_input_table();
            location.assign("/");
        })
        .catch(err => console.error("新增錯誤：", err));
    });

});
