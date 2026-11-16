# Vercel AI SDK DataStream Protocol Specs

The data stream response encodes:
- `0:` Text stream chunks (standard markdown tokens)
- `9:` Tool call initiation with invocation ID and parameter payload
- `a:` Tool execution result returned from server or user
- `2:` Custom annotations (`dataStream.writeMessageAnnotation()`)
- `3:` Custom raw data packets (`dataStream.writeData()`)

By utilizing this multi-channel protocol, the UI handles text streams, tool executions, and metadata in a single HTTP response.
