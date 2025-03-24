(function ($) {
    $(document).ready(function () {
        $('input[name="is_active"]').change(
            function () {
                if (!confirm("Do you really want to change active status?")) {
                    $(this).prop('checked', !$(this).prop('checked'));
                }
            }
        );
    })
})