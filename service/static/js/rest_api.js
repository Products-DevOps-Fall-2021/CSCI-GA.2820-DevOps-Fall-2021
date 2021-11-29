$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product").val(res._id);
        $("#product_name").val(res.name);
        $("#product_description").val(res.description);
        $("#product_price").val(res.price);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_description").val("");
        $("#product_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#product_name").val();
        var description = $("#product_description").val();
        var price = $("#product_price").val();

        var data = {
            "name": name,
            "description": description,
            "price": price
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    $("#search-btn").click(function () {

        var minimum = $("#product_price_minimum").val();
        var maximum = $("#product_price_maximum").val();

        var queryString = ""

        if (minimum) {
            queryString += 'minimum=' + minimum
        }
        if (maximum) {
            if (queryString.length > 0) {
                queryString += '&maximum=' + maximum
            } else {
                queryString += 'maximum=' + maximum
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/products?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:20%">Name</th>'
            header += '<th style="width:40%">Description</th>'
            header += '<th style="width:20%">Creation Date</th>'
            header += '<th style="width:10%">Price</th>'
            header += '<th style="width:10%">Is Active</th>'
            header += '<th style="width:10%">Likes</th></tr>'
            $("#search_results").append(header);
            var firstProduct = "";
            for(var i = 0; i < res.length; i++) {
                var product = res[i];
                var row = "<tr><td>"+product.id+"</td><td>"+product.name+"</td><td>"+product.description+"</td><td>"+product.creation_date+"</td><td>"+product.price+"</td><td>"+product.is_active+"</td><td>"+product.like+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstProduct = product;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });
})
