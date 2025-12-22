class GPUDropletsResourceWithStreamingResponse:

    def __init__(self, gpu_droplets: GPUDropletsResource) -> None:
        self._gpu_droplets = gpu_droplets

    @cached_property
    def backups(self) -> BackupsResourceWithStreamingResponse:
        return BackupsResourceWithStreamingResponse(self._gpu_droplets.backups)

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self._gpu_droplets.actions)

    @cached_property
    def destroy_with_associated_resources(self) -> DestroyWithAssociatedResourcesResourceWithStreamingResponse:
        return DestroyWithAssociatedResourcesResourceWithStreamingResponse(self._gpu_droplets.destroy_with_associated_resources)

    @cached_property
    def autoscale(self) -> AutoscaleResourceWithStreamingResponse:
        return AutoscaleResourceWithStreamingResponse(self._gpu_droplets.autoscale)

    @cached_property
    def firewalls(self) -> FirewallsResourceWithStreamingResponse:
        return FirewallsResourceWithStreamingResponse(self._gpu_droplets.firewalls)

    @cached_property
    def floating_ips(self) -> FloatingIPsResourceWithStreamingResponse:
        return FloatingIPsResourceWithStreamingResponse(self._gpu_droplets.floating_ips)

    @cached_property
    def images(self) -> ImagesResourceWithStreamingResponse:
        return ImagesResourceWithStreamingResponse(self._gpu_droplets.images)

    @cached_property
    def load_balancers(self) -> LoadBalancersResourceWithStreamingResponse:
        return LoadBalancersResourceWithStreamingResponse(self._gpu_droplets.load_balancers)

    @cached_property
    def sizes(self) -> SizesResourceWithStreamingResponse:
        return SizesResourceWithStreamingResponse(self._gpu_droplets.sizes)

    @cached_property
    def snapshots(self) -> SnapshotsResourceWithStreamingResponse:
        return SnapshotsResourceWithStreamingResponse(self._gpu_droplets.snapshots)

    @cached_property
    def volumes(self) -> VolumesResourceWithStreamingResponse:
        return VolumesResourceWithStreamingResponse(self._gpu_droplets.volumes)

    @cached_property
    def account(self) -> AccountResourceWithStreamingResponse:
        return AccountResourceWithStreamingResponse(self._gpu_droplets.account)