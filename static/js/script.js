// 게시물 타임스탬프
function show_timestamp() {
    $.ajax({
        type: "GET",
        url: "/timestamp",
        data: {},
        success: function (response) {
            let rows = response['timestamps']
            for (let i = 0; i < rows.length; i++) {
                let post_id = rows[i]['post_id']
                let timestamp = rows[i]['time']

                console.log(post_id,timestamp)

                $('#timestamp' + post_id).text(timestamp)
            }
        }
    });
}


// DB 자료 요청
function get_data() {
    $.ajax({
        type: 'GET',
        url: '/get_data',
        data: {},
        success: function (response) {

            let rows = response.contents;
            for (let i = 0; i < rows.length; i++) {
                let post_id = rows[i]['post_id']

                hide_show_desc(post_id);

            }
            show_timestamp()
        }
    });
}