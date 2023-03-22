$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();
        var stockname = $('input[name="stockname"]').val();
        $.ajax({
            url: '/get_stock_info',
            method: 'POST',
            data: { stockname: stockname },
            success: function(response) {
                $('#result-area td').eq(0).text(response.stockname);
                $('#result-area td').eq(1).text(response.stocksymbol);
                $('#result-area td').eq(2).text(response.price);
            },
            error: function() {
                alert('Error occurred while getting stock info');
            }
        });
    });

    $('#submit-btn').on('click', function() {
        var shares = $('.spinner input').val();
        $('#shares-input').val(shares);
        $('form').submit();
    });

    (function ($) {
        $('.spinner .btn:first-of-type').on('click', function () {
            $('.spinner input').val(parseInt($('.spinner input').val(), 10) + 1);
        });
        $('.spinner .btn:last-of-type').on('click', function () {
            $('.spinner input').val(parseInt($('.spinner input').val(), 10) - 1);
        });
    })(jQuery);
});