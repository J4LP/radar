module radar {
  'use strict';

  interface IRadarStructuresScope extends ng.IScope {
    structures: Array<IStructure>;
    lastUpdated: Date;
    events: RadarStructuresController;
  }

  export class RadarStructuresController {
    $scope: IRadarStructuresScope;
    Restangular: restangular.IService;
    $modal: ng.ui.bootstrap.IModalService;

    /* @ngInject */
    constructor($scope: IRadarStructuresScope, Restangular: restangular.IService, $modal: ng.ui.bootstrap.IModalService) {
      this.$scope = $scope;
      this.$scope.structures = [];
      this.$scope.events = this;
      this.Restangular = Restangular;
      this.$modal = $modal;
      this.loadStructures();
    }

    loadStructures() {
      this.Restangular.all('structures').getList().then(
        (objects: Array<IStructure>) => {
          this.$scope.structures = objects;
          if (objects.length > 0) {
            this.$scope.lastUpdated = objects[0].updated_on;
          } else {
            this.$scope.lastUpdated = new Date();
          }
        }
      )
    }

    openScanModal(structure: IStructure) {
      var modalInstance = this.$modal.open({
        templateUrl: 'structure_scan_modal.html',
        controller: 'StructureScanModalController',
        resolve: {
          structure: function() {
            return structure;
          }
        }
      });
      modalInstance.result.then(() => {
        this.loadStructures();
      });
    }
  }
}
