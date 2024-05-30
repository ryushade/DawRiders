document.getElementById('deleteButton').addEventListener('click', function() {
    var codmoto = this.getAttribute('data-id');
    var url = this.getAttribute('data-url');
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'codmoto=' + codmoto
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        location.reload();
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
});