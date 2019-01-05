var app = new Vue({
    el: '#app',
    mixins: [utilMixin],
    data: {
        categories: [],
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
        },
    }
})