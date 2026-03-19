export interface TravelErrorProps {
    message: string | null;
}

export default function TravelError({ message }: TravelErrorProps) {
    if (!message) {
        return null;
    }

    return (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-red-500 text-white p-4 rounded-lg opacity-90 text-gray-950 border-2 border-red-800 border-solid">
            {message}
        </div>
    )
}
