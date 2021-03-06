var script = document.createElement('script');
script.type = 'text/javascript';
script.src = 'https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js';
document.head.appendChild(script);
// tinyMCS plugin js code
script.onload = function () {
    tinymce.init({
        selector: '#id_content',
        content_css: '//www.tiny.cloud/css/codepen.min.css',
        width: 600,
        height: 300,
        plugins: [
            'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            'table emoticons template paste help'
        ],
        toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
            'bullist numlist outdent indent | link image | print preview media fullpage | ' +
            'forecolor backcolor emoticons | help',
        menu: {
            favs: { title: 'My Favorites', items: 'code visualaid | searchreplace | spellchecker | emoticons' }
        },
        menubar: 'favs file edit view insert format tools table help'
    });
}