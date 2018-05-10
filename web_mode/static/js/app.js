var wrapper = new Vue({
    el: '#wrapper',
    data: {
        tags: [],
        notebooks: [],
        note: [],
        mode: 'welcome'
    },
    created: function () {
        this.$http.get('/list_notebooks', {}).then(function (response) {
            this.notebooks = response.data;
        });
        this.$http.get('/list_tags', {}).then(function (response) {
            this.tags = response.data;
        });
    },
    mounted: function () {
    },
    methods:{
        note_select: function (title) {
            console.log(title);
            this.$http.get('/get_note?note_title=' + title, {})
                .then(function (response) {
                    this.note = response.data;
                    this.mode = 'view';
            });
        },
        edit_note: function () {
            this.mode = 'edit';

            this.$nextTick(function() {
                if (this.mode == 'edit') {
                    var md = new MdEditor('#note_content');
                    console.log('nextTick');
                }
            });
        },
        edit_cancel: function () {
            this.mode = 'view';
        },
        save_note: function () {
            console.log(this.note.title);
            console.log(this.note.content);
        },
        mv_note: function (notebook_name) {
            console.log(notebook_name)
            this.$http.post('/mv_note', {note_title: this.note.title, notebook_name: notebook_name})
                .then(function (response) {
                    this.$http.get('/list_notebooks', {}).then(function (response) {
                        this.notebooks = response.data;
                    });
                });
        },
        metis_menu: function () {
            $('#side-menu').metisMenu();
        }
    },
    watch:{
        notebooks: function () {
            this.$nextTick(function() {
                this.metis_menu();
            });
        },
        tags: function () {
            this.$nextTick(function() {
                this.metis_menu();
            });
        },
        note: function () {
            $(document).ready(function () {
                $('table').attr('class', 'table table-bordered');
                MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
                console.log('watched');
            });
        },
    }
});
