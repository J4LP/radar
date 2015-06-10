module radar {
  'use strict';

  interface IStructureScanModalControllerScope extends ng.IScope {
    structure: IStructure;
    events: StructureScanModalController;
    editingScan: boolean;
    newScan: string;
  }

  export class StructureScanModalController {
    $scope: IStructureScanModalControllerScope;
    Restangular: restangular.IService;
    $modalInstance: ng.ui.bootstrap.IModalServiceInstance;

    /* @ngInject */
    constructor($scope: IStructureScanModalControllerScope, $modalInstance: ng.ui.bootstrap.IModalServiceInstance, structure: IStructure, Restangular: restangular.IService) {
      this.$scope = $scope;
      this.$scope.structure = structure;
      this.$scope.editingScan = false;
      this.$scope.events = this;
      this.Restangular = Restangular;
      this.$modalInstance = $modalInstance;
    }

    saveScan() {
      this.$scope.structure.customPUT({'scan': this.$scope.newScan}, 'scan').then(() => {
        this.$modalInstance.close();
      })
    }
  }
}
