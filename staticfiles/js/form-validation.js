$(document).ready(function () {
    var rules = {};
    $("form").each(function () {
        var min, max, required = true;
        $(":input").each(function () {
           $.each(this.attributes, function () {

                if(this.name === "min")
                {
                    min = this.value;
                }

                if(this.name === "max")
                {
                    max = this.value;
                }

                rules[this.name] = {
                    required: true,
                    min: min,
                    max: max,
                }
           });
       });

        $(this).validate(
            {
                rules: rules,
                messages: {},

                 highlight: function (element) {
                  $(element).parents(':eq(2)').addClass('alert');
                },

                unhighlight: function (element) {
                    $(element).parents(':eq(2)').removeClass('alert');
                },

                errorPlacement: function (error, element) {
                    return true;
                },
            }
        );

    });
});




