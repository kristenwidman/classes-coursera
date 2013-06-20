$(document).ready(function() {
    $('.showmore').click(function() {
        $( 'table tr:hidden').slice(0,20).show();
        if ( $('table tr').length == $('table tr:visible').length ) {
            $('button').hide();
        }
    });
});
