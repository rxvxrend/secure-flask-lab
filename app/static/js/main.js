const likeButtons = document.querySelectorAll(".like-button");

likeButtons.forEach(button => {

    button.addEventListener("click", async () => {

        const postId = button.dataset.postId;

        const csrfToken = document.querySelector(
            'meta[name="csrf-token"]'
        ).content;

        const response = await fetch(`/like/${postId}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            }
        });

        const data = await response.json();

        document.getElementById(
            `likes-count-${postId}`
        ).innerText = data.likes_count;

        const isLiked = button.dataset.liked === "true";

        if (data.liked) {
            button.innerText = "💔 Unlike";
            button.dataset.liked = "true";
        } else {
            button.innerText = "❤️ Like";
            button.dataset.liked = "false";
        }

    });

});

setTimeout(() => {

    const flashes = document.querySelectorAll(".flash");

    flashes.forEach(flash => {

        flash.classList.add("hide");

        setTimeout(() => {
            flash.remove();
        }, 500);
        
    });

}, 3000);

document.querySelectorAll(".comment-form").forEach(form => {

    form.addEventListener("submit", async (e) => {
    
        e.preventDefault();
    
        const postId = form.dataset.postId;

        const csrfToken = document.querySelector(
            'meta[name="csrf-token"]'
        ).content;

        const input = form.querySelector("input[name='content']");
        const content = input.value;

        if (!content.trim()) {
            return;
        }

        const response = await fetch(`/comments/create/${postId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken
            },
            body: new URLSearchParams({
                content: content
            })
        });

        const data = await response.json();

        const commentsContainer = 
            document.querySelector(`#comments-container-${postId}`);

            const commentHTML = `
                <div class="comment">
                    <b>${data.username}</b>
                    <p>${data.content}</p>
                    <small>${data.created_at}</small>
                </div>
            `;

            commentsContainer.insertAdjacentHTML(
                "afterbegin",
                commentHTML
            );

            input.value = "";
    });
});

document.querySelectorAll(".show-more-comments").forEach(button => {

    button.addEventListener("click", async () => {

        const postId = button.dataset.postId;
        let offset = parseInt(button.dataset.offset);

        const response = await fetch(
            `/comments/more/${postId}?offset=${offset}`
        );

        const data = await response.json();

        const container = document.getElementById(
            `comments-container-${postId}`
        );

        data.forEach(comment => {

            const div = document.createElement("div");
            div.classList.add("comment");

            div.innerHTML = `
                <b>${comment.username}</b>
                <p>${comment.content}</p>
                <small>${comment.created_at}</small>
            `;

            container.appendChild(div);
        });

        offset += data.length;
        button.dataset.offset = offset;

        if (data.length < 5) {
            button.remove();
        }
    });
});