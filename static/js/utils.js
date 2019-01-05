var utilMixin = {
    methods: {
        loadv2(items, callback) {
              // items is an array of loadConfigs 
              // loadConfig = {name, url, variableName, dataInReponse}
              // name- visible name to user in loading text 
              // url - url to hit a get request
              // variableName - save received data back in 
              // dataInReponse - reponse data present in this variable
              var vm = this
              var taskCount = items.length
  
              var receviedData = {}
              var names = []
  
              items.forEach(item => {
                  names.push(item.name)
              })
  
              var errorMessage = undefined
              var errors = {}
  
              var updateLoadingMessage = function () {
                  if (names.length > 0) {
                      suffix = names.join(', ')
                      vm.loading = 'loading ' + suffix + '...'
                  } else
                      vm.loading = undefined
              }
              updateLoadingMessage() // set loading message
  
              var setAllToVm = function () {
                  updateLoadingMessage()
                  if (taskCount == 0) {
                      if (errorMessage) {
                          vm.error = errorMessage
                      } else {
                          items.forEach(item => {
                              vm[item.variableName] = receviedData[item.dataInReponse] || item.default
                          })
                          vm.error = ''
                      }
                      vm.loading = undefined
                      console.log('done loading')
                      if (callback) {
                          callback()
                      }
                  }
              }
              var showError = function () {
                  updateLoadingMessage()
                  var errored = []
                  items.forEach(item => {
                      if (errors[item.name]) {
                          errored.push(item.name)
                      }
                  })
                  if (errored.length > 0) {
                      suffix = errored.join(', ')
                      errorMessage = 'Error occured in loading ' + suffix + ' please reload the page'
                  }
                  if (taskCount == 0) {
                      vm.error = errorMessage
                      vm.loading = undefined
                      console.log('done loading')
                  }
              }
  
              var getErrorText = function (error) {
                  if (error.body)
                      return error.body.message || error.statusText
                  return error.statusText
              }
  
              items.forEach(item => {
                  vm.$http.get(item.url)
                      .then(response => {
                              taskCount -= 1
                              names.pop(names.indexOf(item.name))
                              if (response.body) {
                                if(item.dataInReponse){
                                    receviedData[item.dataInReponse] = response.body[item.dataInReponse]
                                } else {
                                    receviedData[item.dataInReponse] = response.body
                                }
                              }
                              setAllToVm()
                          },
                          error => {
                              console.log(error)
                              taskCount -= 1
                              names.pop(names.indexOf(item.name))
                              errors[item.name] = getErrorText(error)
                              showError()
                          })
              })
        }
    }
}