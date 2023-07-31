const board_number = window.location.pathname.split('/board/')[1]

$.ajax({
    "url": `/api/v1/boards/board/${board_number}`,
    "method": "GET",
    "timeout": 0,
}).done(function (board) {
    console.log(board);
    $('#author').text(board.author === null ? 'anonymous' : board.author.username);
    $('#title').val(board.title);
    $('#content').val(board.content);
    $('#file').attr('src', board.file);
    $('#create_at').val(board.create_at);
    $('#update_at').val(board.update_at);

    var languagechk = $('#languagechk');
    if (board.file) {
        languagechk.show();
    }else{
        languagechk.hide();
    }
});

function changetxt() {
    var kor = $('#kor').is(':checked');
    var eng = $('#eng').is(':checked');
    var jpn = $('#jpn').is(':checked');
    console.log("한국어 선택 : "+kor);
    console.log("영어 선택 : "+eng);
    console.log("일본어 선택 : "+jpn);
}