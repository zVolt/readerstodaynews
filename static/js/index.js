var app = new Vue({
    el: '#app',
    data: {
        title: 'Readers Today News',
        tags: [],
        main_post: {
          media_items: [ { image: undefined}]
        },
        primary_posts: [],
        old_posts: [],
    },
    created: function(){
      this.get_posts()
      this.get_tags()
    },
    updated: function(){
    },
    computed: {
      top_tags: function(){
        return this.tags.splice(0, 5)
      }
    },
    methods: {
      posts_updated: function(all_posts){
        var vm = this
        vm.main_post = all_posts[0]
        vm.primary_posts = all_posts.slice(1, 3)
        vm.old_posts = all_posts.slice(3)
      },
      get_tags: function(){
        var vm = this
        axios.get('/api/tag/list').then(
          response=>{
            vm.tags = response.data
          },
          error=>{
            console.log(error)
          })
      },
      get_posts: function(){
        var vm = this
        axios.get('/api/post/list?limit=30').then(
        response=>{
          vm.posts_updated(response.data.results)
        },
        error=>{
          console.log(error)
        })
      }
    }
    })






