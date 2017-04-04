data = {};
tags = [{val: "ALLERGY", desc: "Allergy"}, {val: "DISEASE", desc: "Disease"}, {val: "METRIC", desc: "Metric"},
        {val: "NAME", desc: "Name"}, {val: "NUMBER", desc: "Number | Quantity of metric"},
        {val: "OTHERS", desc: "Others"}, {val: "PLACE", desc: "Place"}, {val: "SYMPTOM", desc: "Symptom"},
        {val: "TIME", desc: "Time"}, {val: "UNIT", desc: "Unit | Unit of Metric"}, {val: "VACCINE", desc: "Vaccine"}];

select = '';
$(document).ready(function() {
    ls = '';
    for(tag in tags) {
        select += "<option value=\""+tags[tag]["val"]+"\">"+tags[tag]["val"]+"</option>";
        ls += "<li><b><u>"+tags[tag]["val"]+"</b></u>: "+tags[tag]["desc"]+"</li>";
    }
    $("#list-tags").html(ls);
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
        autoAccept: true,
        preventPaste: false,

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
        str+= "<div class=\"d1\">"+words[i]+"</div>&nbsp;<div class=\"d1\"><select id=\""+id+i+"\" class=\"form-control\" style=\"width: auto;\"><option value=\"NA\" selected disabled>Select Tag</option>"+select+"</select></div>&emsp;";
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
        autoAccept: true,
        preventPaste: false,

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

function sub() {
    var d = {"tagged":[]};
    for(i in data) {
        var str = '';
        for(j=0;j<data[i].length;++j) {
            str += data[i][j]+'/'+$("#"+i+j).val()+' ';
        }
        d["tagged"].push(str);
    }
    $("#data").val(JSON.stringify(d));
    $("#form").submit();
}