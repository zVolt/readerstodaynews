var app = new Vue({
    el: '#app',
    mixins: [utilMixin],
    data: {
        // dummy variable to hold the result from which post will be extracted
        posts: [],
        post: {},
        postid: postid,
    },
    created: function(){
        this.loadv2([
            {
                name: 'Post',
                url: '/api/post/list?detailed=true&ids='+postid,
                variableName: 'posts',
                dataInReponse: 'results'
            },
        ], this.init)
    },
    computed: function(){},
    methods:{
        init: function(){
            if(this.posts && this.posts.length){
                this.post = this.posts[0]
            }
            if(this.post){
                $('.headerimage img').attr('src', this.post.media_items[0].image)
            }
        }
    }
})