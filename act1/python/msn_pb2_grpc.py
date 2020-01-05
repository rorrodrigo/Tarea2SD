# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import msn_pb2 as msn__pb2


class ServidorMSNStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.RecibirMensaje = channel.unary_stream(
        '/ServidorMSN/RecibirMensaje',
        request_serializer=msn__pb2.Usuario.SerializeToString,
        response_deserializer=msn__pb2.Mensaje.FromString,
        )
    self.EnviarMensaje = channel.unary_unary(
        '/ServidorMSN/EnviarMensaje',
        request_serializer=msn__pb2.Mensaje.SerializeToString,
        response_deserializer=msn__pb2.Ack.FromString,
        )
    self.DevolverUsuarios = channel.unary_unary(
        '/ServidorMSN/DevolverUsuarios',
        request_serializer=msn__pb2.Usuario.SerializeToString,
        response_deserializer=msn__pb2.Usuario.FromString,
        )
    self.ValidarUsuario = channel.unary_unary(
        '/ServidorMSN/ValidarUsuario',
        request_serializer=msn__pb2.Usuario.SerializeToString,
        response_deserializer=msn__pb2.Ack.FromString,
        )
    self.DevolverMensajes = channel.unary_stream(
        '/ServidorMSN/DevolverMensajes',
        request_serializer=msn__pb2.Usuario.SerializeToString,
        response_deserializer=msn__pb2.Mensaje.FromString,
        )
    self.Desconectarse = channel.unary_unary(
        '/ServidorMSN/Desconectarse',
        request_serializer=msn__pb2.Usuario.SerializeToString,
        response_deserializer=msn__pb2.Ack.FromString,
        )


class ServidorMSNServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def RecibirMensaje(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def EnviarMensaje(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DevolverUsuarios(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ValidarUsuario(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DevolverMensajes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Desconectarse(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ServidorMSNServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'RecibirMensaje': grpc.unary_stream_rpc_method_handler(
          servicer.RecibirMensaje,
          request_deserializer=msn__pb2.Usuario.FromString,
          response_serializer=msn__pb2.Mensaje.SerializeToString,
      ),
      'EnviarMensaje': grpc.unary_unary_rpc_method_handler(
          servicer.EnviarMensaje,
          request_deserializer=msn__pb2.Mensaje.FromString,
          response_serializer=msn__pb2.Ack.SerializeToString,
      ),
      'DevolverUsuarios': grpc.unary_unary_rpc_method_handler(
          servicer.DevolverUsuarios,
          request_deserializer=msn__pb2.Usuario.FromString,
          response_serializer=msn__pb2.Usuario.SerializeToString,
      ),
      'ValidarUsuario': grpc.unary_unary_rpc_method_handler(
          servicer.ValidarUsuario,
          request_deserializer=msn__pb2.Usuario.FromString,
          response_serializer=msn__pb2.Ack.SerializeToString,
      ),
      'DevolverMensajes': grpc.unary_stream_rpc_method_handler(
          servicer.DevolverMensajes,
          request_deserializer=msn__pb2.Usuario.FromString,
          response_serializer=msn__pb2.Mensaje.SerializeToString,
      ),
      'Desconectarse': grpc.unary_unary_rpc_method_handler(
          servicer.Desconectarse,
          request_deserializer=msn__pb2.Usuario.FromString,
          response_serializer=msn__pb2.Ack.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ServidorMSN', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
