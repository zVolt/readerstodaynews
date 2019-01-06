var app = new Vue({
    el: '#app',
    mixins: [utilMixin],
    data: {
        categories: [],
        posts_by_cat: {},
    },
    created: function(){
        // name- visible name to user in loading text 
        // url - url to hit a get request
        // variableName - save received data back in 
        // dataInReponse - reponse data present in this variable
        this.loadv2([
            {
                name: 'Categories',
                url: '/api/tag/list',
                variableName: 'categories',
                dataInReponse: ''
            },
        ], this.init)
    },
    methods:{
        init: function(){
            console.log(this.categories)
            this.categories.forEach(cat => {
                this.load_posts(cat)
            });
        },
        load_posts: function(cat){
            var vm = this
            axios.get('/api/post/list?tags='+cat.name).then(
                response => {
                    console.log(response)
                    vm.$set(vm.posts_by_cat, cat.id, response.data.results)
                },
                error => {
                    console.log(error)
                }
            )
        }
    }
})