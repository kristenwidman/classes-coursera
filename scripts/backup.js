

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9/jquery.min.js"></script>
    <script>
        $(document).ready(function() {
            $('ul li:gt(9)').hide();
            $('.showmore').on('click', function() {
                //$('.row').filter('.hidden').removeClass('.hidden');
                $('ul li:gt(9)').show();
            });
        });
    </script>
