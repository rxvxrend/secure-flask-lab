const likeButtons = document.querySelectorAll(".like-button");

likeButtons.forEach(button => {

    button.addEventListener("click", async () => {

        const postId = button.dataset.postId;

        const responce = await fetch(`/like/${postId}`, {
            method: "POST"
        });

        const data = await responce.json();

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
        flash.style.display = "none";
    });

}, 3000);
