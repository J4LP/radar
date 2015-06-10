module radar {
  'use strict';

  interface IAddStructureScope extends ng.IScope {
    events: AddStructureController;
    structure: IStructure;
    addStructureForm: ng.IFormController;
  }

  export class AddStructureController {
    $scope: IAddStructureScope;
    Restangular: restangular.IService;
    $location: ng.ILocationService;
    $http: ng.IHttpService;
    callback_url: string;

    /* @ngInject */
    constructor($scope: IAddStructureScope, Restangular: restangular.IService, $location: ng.ILocationService, $http: ng.IHttpService) {
      this.$scope = $scope;
      this.$scope.events = this;
      this.Restangular = Restangular;
      this.$location = $location;
      this.$http = $http;
    }

    init(callback_url) {
      this.callback_url = callback_url;
    }

    saveStructure() {
      console.log('foo');
      this.Restangular.all('structures').post(this.$scope.structure).then(
        (structure: IStructure) => {
          window.location.replace(this.callback_url);
        }, (error: IErrorResponse) => {
          console.log(error);
          //swal('Error!', data.error ? data.error : 'Unknown server error.', 'error');
        }
      )
    }

    getSystem(query) {
      return this.$http.post('/api/autocomplete/systems', {query: query}).then(function (response: any) {
        return response.data.map(function (system) {
          return system.name
        })
      })
    }

    getEveType(query) {
      return this.$http.post('/api/autocomplete/evetypes', {query: query}).then(function (response: any) {
        return response.data.map(function (system) {
          return system.name
        })
      })
    }
  }
}
