function submit(id) {
    $.post("/get_country_list", { "netflixid": id }, function (data) {
        $("#modal-body").html(data);
        $("#countryModal").modal();
    });
}

function change_country(country, country_name) {
    $.post("/change_country", { "country": country }, function (data) {
        // Creating array out of the data
        let result = JSON.parse(data);
        let final_result = create_results(result);
        $("#original-results").hide()
        $("#ajax-results").html(final_result);
        $("#country-results").html("Here are the results for " + country_name);
    })
}

function create_results(result) {

    let final_result = "";
    for (let i = 0; i < result.length; i++) {

        let obj = result[i];

        let netflixid = obj.netflixid;
        let image;
        if (obj.large_image) {
            image = obj.large_image;
        } else {
            image = obj.image;
        }
        let title = obj.title;
        let release_date = obj.release_date;
        let rating;
        if (obj.rating && obj.rating != 0) {
            rating = obj.rating;
        } else {
            rating = 'N/A'
        }
        let time;
        if (obj.time) {
            time = obj.time;
        } else {
            time = 'N/A'
        }
        let synopsis = obj.synopsis;
        let link = obj.link;

        let first_part =
            `<div class="card mb-3 fliks-results" style="margin-bottom: 0.3rem !important;">
            <div class="row no-gutters">
                <div class="col-md-4">
                    <img src="${image}" class="card-img" alt="${title}">
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                        <h5 class="card-title">${title}  (${release_date})</h5>
                        <h6 class="card-subtitle mb-2 text-muted" style="margin-bottom: 0"> Rating: ${rating} Time: ${time}
                        </h6>
                        <p class="card-text" style="margin-bottom:0">${synopsis}</p>
                        <a href="${link}" target="_blank" class="btn btn-link">Watch</a>
                        <button class="btn btn-link" onclick="submit(${netflixid})">Country details</button>`

        let closing_tags = `</div></div></div></div>\n`
        if (obj.download == 1) {
            let downloadble = `<p class="card-text"><small class="text-muted">This content is downloadable</small></p>`
            final_result += first_part + downloadble + closing_tags;
        } else {
            final_result += first_part + closing_tags;
        }
    }

    return final_result

}


$(document)
    .ajaxStart(function () {
        $("#loading").modal('show');
    })
    .ajaxStop(function () {
        $("#loading").modal('hide');
    });