function submit(id) {
  $.post("/get_country_list", { netflixid: id }, function (data) {
    $("#modal-body").html(data);
    $("#countryModal").modal();
  });
}

function change_country(country, country_name) {
  $.post("/change_country", { country: country }, function (data) {
    // Creating array out of the data
    const result = JSON.parse(data);
    const final_result = create_results(result);
    $("#original-results").hide();
    $("#ajax-results").html(final_result);
    $("#country-results").html("Here are the results for " + country_name);
  });
}

function create_results(result) {
  let final_result = "";
  for (let i = 0; i < result.length; i++) {
    const obj = result[i];

    const netflixid = obj.netflixid;

    let image = "None";

    if (obj.large_image) {
      image = obj.large_image;
    } else {
      image = obj.image;
    }
    const title = obj.title;
    const release_date = obj.release_date;
    let rating;
    if (obj.rating && obj.rating != 0) {
      rating = obj.rating;
    } else {
      rating = "N/A";
    }
    let time;
    if (obj.time) {
      time = obj.time;
    } else {
      time = "N/A";
    }
    const synopsis = obj.synopsis;
    const link = obj.link;

    const first_part = `<div class="card mb-3 fliks-results" style="margin-bottom: 0.3rem !important;">
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
                        <button class="btn btn-link" onclick="submit(${netflixid})">Country details</button>`;

    const closing_tags = `</div></div></div></div>\n`;
    if (obj.download == 1) {
      const downloadble = `<p class="card-text"><small class="text-muted">This content is downloadable</small></p>`;
      final_result += first_part + downloadble + closing_tags;
    } else {
      final_result += first_part + closing_tags;
    }
  }

  return final_result;
}

function ondemand_change_country(term, country) {
  $.post(
    "/ondemand_change_country",
    { search: term, country: country },
    function (data) {
      const ondemand_results = construct_ondemand_results(JSON.parse(data));
      $("#original-results").hide();
      if (ondemand_results) {
        $("#ajax-results").html(ondemand_results);
      } else {
        $("#ajax-results").html("<h1>Not Available</h1>");
      }
      let search_country = country.toUpperCase();
      $("#ondemand-results").html(
        `Here is the result for "${term}" in ${search_country}`
      );
    }
  );
}

function construct_ondemand_results(data) {
  if (!data) {
    return false;
  }

  let ondemand_results = "";
  data.forEach((element) => {
    const name = element.name;
    let picture = '<p class="card-text non-picture">Image is not available</p>';
    first_part = '<div class="card mb-3">';
    if (element.picture) {
      first_part += `<img src=${element.picture} class="card-img-top">`;
    } else {
      first_part += picture;
    }

    const name_part = `
        <div class="card-body">
	    <h5 class="card-title">${name}</h5>
        <p class="card-text">Here are the current services that have ${name} on:</p>
        `;

    let locations = "";
    element.locations.forEach((location) => {
      location_tag = "";
      if (location[1] === null) {
        location_tag = `<img src=${location[2]} alt=${location[0]}>`;
      } else {
        location_tag = `<a href=${location[1]}><img src=${location[2]} alt=${location[0]}></a>`;
      }
      locations += location_tag;
    });

    const closing_tags = "</div></div>";

    ondemand_results += first_part + name_part + locations + closing_tags;
  });

  return ondemand_results;
}

$(document)
  .ajaxStart(function () {
    $("#loading").modal("show");
  })
  .ajaxStop(function () {
    $("#loading").modal("hide");
  });
