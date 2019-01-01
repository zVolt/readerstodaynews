
var menuMixin = {
    data:  function () {
        return {
            name: 'Readers Today News',
            items: [{
                name: 'Home',
                url: '/index'
            },{
                name: 'About',
                url: '/about'
            }]
        }
    },
    created: function(){
        $('.ui.sidebar')
        .sidebar({
            context: $('.bottom.segment')
        })
        .sidebar('setting', 'transition', 'overlay')
        .sidebar('attach events', '#sidebar-button');
    }
}

var mainMenu = new Vue({
    el: '#menu',
    mixins: [menuMixin],
    data: {
    },
    created: function(){
        this.get_tags()
    },
    methods:{
        add_tags_items_to_menu: function(tags){
            tags.forEach(tag => {
                this.items.push({name: tag.name, url: '/section/'+tag.name, active: false})
            });
        },
        get_tags: function(){
            var vm = this
            axios.get('/api/tag/list').then(
            response=>{
                console.log(response)
                vm.add_tags_items_to_menu(response.data)
            },
            error=>{
                console.log(error)
            })
        }
    }
})