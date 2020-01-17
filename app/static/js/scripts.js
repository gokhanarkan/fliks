function submit(id) {
    $.post("/get_country_list", {"netflixid": id}, function(data){
        $("#modal-body").html(data);
        $("#countryModal").modal();
    });
}

$(document)
    .ajaxStart(function () {
        $("#loading").modal('show');
    })
    .ajaxStop(function () {
        $("#loading").modal('hide');
    });