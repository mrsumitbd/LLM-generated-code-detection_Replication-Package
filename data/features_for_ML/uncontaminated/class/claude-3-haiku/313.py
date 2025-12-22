from cached_property import cached_property

class GPUDropletsResourceWithStreamingResponse:
    def __init__(self, gpu_droplets: GPUDropletsResource) -> None:
        self.gpu_droplets = gpu_droplets

    @cached_property
    def backups(self) -> BackupsResourceWithStreamingResponse:
        return BackupsResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def destroy_with_associated_resources(self) -> DestroyWithAssociatedResourcesResourceWithStreamingResponse:
        return DestroyWithAssociatedResourcesResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def autoscale(self) -> AutoscaleResourceWithStreamingResponse:
        return AutoscaleResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def firewalls(self) -> FirewallsResourceWithStreamingResponse:
        return FirewallsResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def floating_ips(self) -> FloatingIPsResourceWithStreamingResponse:
        return FloatingIPsResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def images(self) -> ImagesResourceWithStreamingResponse:
        return ImagesResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def load_balancers(self) -> LoadBalancersResourceWithStreamingResponse:
        return LoadBalancersResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def sizes(self) -> SizesResourceWithStreamingResponse:
        return SizesResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def snapshots(self) -> SnapshotsResourceWithStreamingResponse:
        return SnapshotsResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def volumes(self) -> VolumesResourceWithStreamingResponse:
        return VolumesResourceWithStreamingResponse(self.gpu_droplets)

    @cached_property
    def account(self) -> AccountResourceWithStreamingResponse:
        return AccountResourceWithStreamingResponse(self.gpu_droplets)