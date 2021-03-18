//function check_parameters(info_id) {
//$(document).ready(function() {
//    $("#add_cart_form").submit(function(event){
//        let all_params = document.querySelectorAll('input[type="radio"].product_parameters');
//        let unique_params_name = new Set(Array.from(all_params, el => el.name));
//        let params_id = [];
//
//        unique_params_name.forEach(function(item, i, arr) {
//            let checked_param = $( all_params ).filter('input[name="'+item+'"][checked]');
//            if (checked_param.length > 0) {
//                params_id.push(checked_param.attr("id"));
//            }
//            else {
//                $("div.parameters_item_" + item + '"').append("Необходимо выбрать значение!");
//                return false;
//            }
//        });
//
//        $.ajax({
//            url: "{% url 'records:get_product' %}",
//            type: "POST",
//            datatype: "json",
//            data: {
//                info_id: info_id,
//                params_id: params_id},
//            success: function(response){
//                    $("#div").html(response);
//                    console.log("There is a response");
//            },
//            error: function (response) {
//                alert(response["responseJSON"]["error"]);
//            },
//        });
//    });
//});


$(document).ready(function() {


    // При нажатии на кнопку "В корзину" запустить проверку
    $("#add_cart_form").submit(function(event) {

        let check_params = true; // предположим выбраны все параметры
        // выбрать все доступные параметры
        let all_params = document.querySelectorAll('input[type="radio"].product_parameters');
        // выбрать группы параметров
        let unique_params_name = new Set(Array.from(all_params, el => el.name));

        let frm = $("#add_cart_form");
        form_data = $(frm).serializeArray();
        // по каждой группе параметров осуществить проверку выбора
        unique_params_name.forEach(function(item, i, arr) {
            let checked_param = $( all_params ).filter('input[name="'+item+'"][checked]');
            if (checked_param.length > 0) {
                form_data.push({ name:'params_id[]' , value: checked_param.attr("id") });
            }
            else {
                $("div.parameters_item_" + item + '"').append("Необходимо выбрать значение!");
                check_params = false;
            }
        });

        // если все параметры указаны, найти товар и добавить в корзину
        if (check_params) {
            $.post(frm.attr('action'),form_data
                    )
              .done(function( data ) {
                alert( "Товар в корзинке: " + data);
              })
              .fail(function(err) {
                alert( "Возникли проблемы при добавлении товара в корзину! " );
            });
             event.preventDefault();
         }
         return false;
    });
});


