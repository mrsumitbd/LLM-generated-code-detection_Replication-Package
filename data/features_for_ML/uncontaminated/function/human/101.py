from verl.protocol import DataProtoFuture
from verl.protocol import DataProto
from verl.protocol import DataProto, DataProtoFuture
from verl.protocol import DataProto, DataProtoFuture
from verl.protocol import DataProto
from verl.protocol import DataProto

def _split_args_kwargs_data_proto(chunks, *args, **kwargs):
    from verl.protocol import DataProto, DataProtoFuture
    splitted_args = []
    for arg in args:
        assert isinstance(arg, (DataProto, DataProtoFuture))
        splitted_args.append(arg.chunk(chunks=chunks))

    splitted_kwargs = {}
    for key, val in kwargs.items():
        assert isinstance(val, (DataProto, DataProtoFuture))
        splitted_kwargs[key] = val.chunk(chunks=chunks)

    return splitted_args, splitted_kwargs