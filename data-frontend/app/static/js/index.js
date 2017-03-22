data = {}
$(document).ready(function() {
    $(":input[type='text']").keyboard({
        language: ['hi'],
        rtl: false,
        layout: 'ms-Devanagari - INSCRIPT',
        reposition: true,
        usePreview: false,
        alwaysOpen: false,
        initialFocus: true,
        noFocus: false,
        stayOpen: false,
        userClosed: false,
        ignoreEsc: false,
        lockInput: true,
        autoAccept: true,

        position: {
            of: $("#keyboard"),
            my: 'center top',
            at: 'center top',
            at2: 'center bottom'
        },
        accepted: function(e, keyboard, el) {

        }
    });
});
function tag_sentence(id) {
    var sentence = $("#"+id).val();
    var words = sentence.split(" ");
    var str = "<div class=\"col-md-12\">"
    for(i in words) {
        if(!words[i]) continue;
        str+= "<div class=\"d1\">"+words[i]+"</div>&nbsp;<div class=\"d1\"><select id=\""+id+i+"\" class=\"form-control\" style=\"width: auto;\"><option value=\"\" selected disabled>Select Tag</option><option>1</option></select></div>&emsp;";
    }
    data[id] = words;
    str += "<button class=\"btn btn-primary\" onclick=\"edit('"+id+"', '"+sentence+"');\"> Edit </button></div>";
    $("#d"+id).html(str);
}

function edit(id, sentence) {
    delete data[id];
    str = "<div class=\"col-md-11\"><input type=\"text\" class=\"form-control\" id=\""+id+"\" value=\""+sentence+"\"></div><div class=\"col-md-1\"><button class=\"btn btn-primary\" onclick=\"tag_sentence('"+id+"');\">Tag</button></div>";
    $("#d"+id).html(str);
    $(":input[type='text']").keyboard({
        language: ['hi'],
        rtl: false,
        layout: 'ms-Devanagari - INSCRIPT',
        reposition: true,
        usePreview: false,
        alwaysOpen: false,
        initialFocus: true,
        noFocus: false,
        stayOpen: false,
        userClosed: false,
        ignoreEsc: false,
        lockInput: true,
        autoAccept: true,

        position: {
            of: $("#keyboard"),
            my: 'center top',
            at: 'center top',
            at2: 'center bottom'
        },
        accepted: function(e, keyboard, el) {

        }
    });
}