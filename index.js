const Serialport = require('serialport')
const Delimiter = Serialport.parsers.Delimiter
const port = new Serialport('/dev/ttyACM0', {
    autoOpen: true,
    baudRate: 9600,
})
const { DynamoDB } = require('aws-sdk')
const client = new DynamoDB.DocumentClient({region: 'eu-west-1'})

const parser = port.pipe(new Delimiter({delimiter: '}', includeDelimiter: true}))
const format = require('date-fns/formatISO')

parser.on('data', async data => {
    try {
        const {temperature, humidity } = JSON.parse(data.toString('utf8'))

        if(!temperature || !humidity){
            return
        }

        const timestamp = format(Date.now())
        const Item = {timestamp, temperature, humidity}

        const res = await client.put({TableName: 'house-metrics', Item}).promise()
    }catch(e){
        console.log('error: ', e.message)
    }
})